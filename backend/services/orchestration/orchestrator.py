import logging
from backend.schemas.checkin import DailyCheckInRequest, DailyCheckInResponse, MultiAgentAnalysis
from backend.services.agents.conversation_agent import ConversationAgent
from backend.services.agents.emotion_agent import EmotionAgent
from backend.services.agents.intent_agent import IntentAgent
from backend.services.agents.longitudinal_agent import LongitudinalAgent
from backend.services.agents.memory_agent import MemoryAgent
from backend.services.agents.milestone_agent import MilestoneAgent
from backend.services.agents.recommendation_agent import RecommendationAgent
from backend.services.agents.safety_agent import SafetyAgent
from backend.services.ai.gemini_client import GeminiClient, GeminiClientError
from backend.services.ai.prompt_builder import PromptBuilder
from backend.services.ai.response_parser import (
    build_fallback_analysis,
    parse_agent_response,
)

logger = logging.getLogger(__name__)


class CheckInOrchestrator:
    def __init__(
        self,
        gemini_client: GeminiClient | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        self.gemini_client = gemini_client or GeminiClient()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.safety_agent = SafetyAgent()
        self.intent_agent = IntentAgent()
        self.emotion_agent = EmotionAgent()
        self.memory_agent = MemoryAgent()
        self.milestone_agent = MilestoneAgent()
        self.longitudinal_agent = LongitudinalAgent()
        self.recommendation_agent = RecommendationAgent()
        self.conversation_agent = ConversationAgent()

    async def run_daily_check_in(self, payload: DailyCheckInRequest) -> DailyCheckInResponse:
        local_safety = self.safety_agent.pre_screen(payload.journal_entry)
        if local_safety.crisis_detected:
            logger.info("Local safety prescreen triggered crisis detection.")
            fallback = build_fallback_analysis(payload, safe_support_mode=True)
            updated_memory = self.memory_agent.update(
                payload.memory,
                fallback.memory_updates,
                fallback.milestone_events,
                fallback.emotional_analysis,
                fallback.longitudinal_patterns,
            )
            return DailyCheckInResponse(
                status="completed",
                source="fallback",
                analysis=fallback,
                updated_memory=updated_memory,
            )

        try:
            model_name = getattr(getattr(self.gemini_client, "settings", None), "ai_model", "unknown")
            logger.info("Gemini request started with model: %s", model_name)
            prompt = self.prompt_builder.build_daily_check_in_prompt(payload)
            raw_output = await self.gemini_client.generate_structured_output(
                prompt=prompt,
                schema=MultiAgentAnalysis.model_json_schema(),
            )
            logger.info("Gemini structured response received")
            parsed_analysis = parse_agent_response(raw_output)
            logger.info("Response parsing successful")
            source = "ai"
        except (GeminiClientError, ValueError) as exc:
            logger.error("Gemini request or parsing failed: %s", str(exc))
            logger.info("Fallback safety response triggered")
            parsed_analysis = build_fallback_analysis(payload, safe_support_mode=False)
            source = "fallback"

        final_safety = self.safety_agent.enforce(local_safety, parsed_analysis.safety_assessment)
        intent = self.intent_agent.process(parsed_analysis.intent_analysis)
        emotion = self.emotion_agent.process(parsed_analysis.emotional_analysis, payload)
        milestones = self.milestone_agent.process(parsed_analysis.milestone_events)
        longitudinal = self.longitudinal_agent.process(parsed_analysis.longitudinal_patterns)
        recommendations = self.recommendation_agent.process(
            parsed_analysis.recommendations,
            final_safety,
            emotion,
        )
        conversation = self.conversation_agent.process(
            parsed_analysis.conversation_response,
            final_safety,
            emotion,
        )

        if final_safety.safe_support_mode:
            recommendations = self.safety_agent.soften_recommendations(recommendations)
            conversation = self.safety_agent.soften_conversation(conversation)

        final_analysis = parsed_analysis.model_copy(
            update={
                "safety_assessment": final_safety,
                "intent_analysis": intent,
                "emotional_analysis": emotion,
                "milestone_events": milestones,
                "longitudinal_patterns": longitudinal,
                "recommendations": recommendations,
                "conversation_response": conversation,
            }
        )

        updated_memory = self.memory_agent.update(
            payload.memory,
            final_analysis.memory_updates,
            final_analysis.milestone_events,
            final_analysis.emotional_analysis,
            final_analysis.longitudinal_patterns,
        )

        return DailyCheckInResponse(
            status="completed",
            source=source,
            analysis=final_analysis,
            updated_memory=updated_memory,
        )
