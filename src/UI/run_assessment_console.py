from dotenv import load_dotenv
import os
import sys
import logging
import json
import pathlib as Path

import crewai as crewai
import langchain_openai as lang_oai
import crewai_tools as crewai_tools
from src.Helpers.pretty_print_crewai_output import display_crew_output
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource


from src.Agents.biomechanics_coach_agent import BiomechanicsCoachAgent
from src.Agents.conditioning_coach_agent import ConditioningCoachAgent
from src.Agents.motivator_agent import MotivatorAgent
from src.Agents.nutrition_agent import NutritionAgent
from src.Agents.physiology_agent import PhysiologyAgent
from src.Agents.position_coach_agent import PositionCoachAgent
from src.Agents.psychology_agent import PsychologyAgent
from src.Agents.comprehensive_report_agent import ComprehensiveReportAgent
from src.Agents.exercise_database_agent import ExerciseDatabaseAgent
from src.Agents.fitbit_agent import FitbitAgent
from src.Agents.athlete_profile_agent import AthleteProfileAgent

import src.Utils.utils as utils

# Load environment variables
load_dotenv("/etc/secrets")

# Initialize logger
logger = utils.configure_logger(logging.INFO)
from src.Helpers.athlete_example_profiles import jane_smith_tennis, john_doe_soccer



class AssessmentCrew:
    def __init__(self, input_file_path="data/athlete_profile.txt"):        
        self.knowledge_data = utils.get_knowledge_type(input_file_path)

    def run(self):
        # Initialize agents with the player profile
        biomechanics_coach_agent = BiomechanicsCoachAgent(athlete_profile=jane_smith_tennis)
        conditioning_coach_agent = ConditioningCoachAgent(athlete_profile=jane_smith_tennis)
        exercise_database_agent = ExerciseDatabaseAgent(athlete_profile=jane_smith_tennis)
        #fitbit_agent = FitbitAgent(athlete_profile=jane_smith_tennis)
        motivator_agent = MotivatorAgent(athlete_profile=jane_smith_tennis)
        nutrition_agent = NutritionAgent(athlete_profile=jane_smith_tennis)
        physiology_agent = PhysiologyAgent(athlete_profile=jane_smith_tennis)
        position_coach_agent = PositionCoachAgent(athlete_profile=jane_smith_tennis)
        psychology_agent = PsychologyAgent(athlete_profile=jane_smith_tennis)
        comprehensive_report_agent = ComprehensiveReportAgent(athlete_profile=jane_smith_tennis)
        athlete_profile_agent = AthleteProfileAgent(athlete_profile=jane_smith_tennis)

        agents = [
            biomechanics_coach_agent, 
            conditioning_coach_agent,
            exercise_database_agent,
            #fitbit_agent,
            motivator_agent,
            nutrition_agent,
            physiology_agent,
            position_coach_agent,
            psychology_agent,
            comprehensive_report_agent,
            athlete_profile_agent
        ]

        tasks = [
            biomechanics_coach_agent.analyze_biometrics(),
            conditioning_coach_agent.create_conditioning_program(),
            exercise_database_agent.recommend_exercises(),
            #fitbit_agent.analyze_data(),
            motivator_agent.motivate_athlete(),
            nutrition_agent.generate_meal_plan(),
            physiology_agent.generate_physiology_report(),
            position_coach_agent.generate_position_advice(),
            psychology_agent.generate_psychology_report(),
            comprehensive_report_agent.compile_report(),
            athlete_profile_agent.provide_athlete_profile()
        ]
        

        # Run tasks
        crew = crewai.Crew(
            agents=agents,
            tasks=tasks,
            knowledge_sources=[self.knowledge_data],
            process=crewai.Process.sequential,
            verbose=True
        )

        # Register crew with BaseAgent        
        for agent in crew.agents:
            logger.info(f"Agent Name: '{agent.role}'")
            agent.register_crew(crew)

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Assessment Analysis")
    print('-------------------------------')

    assessment_crew = AssessmentCrew()
    logger.info("Assessment crew initialized successfully")

    try:
        crew_output = assessment_crew.run()
        #crew_output = assessment_crew.run(inputs={"job": "Create a comprehensive overview of the athlete"})
        logger.info("Assessment crew execution run() successfully")
    except Exception as e:
        logger.error(f"Error during crew execution: {e}")
        sys.exit(1)

    # Display the output
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")

    display_crew_output(crew_output)

    print("Collaboration complete")
    sys.exit(0)
