import crewai as crewai
import json
from textwrap import dedent
from src.Agents.base_agent import BaseAgent
from src.Helpers.athlete_profile import AthleteProfile


class NutritionAgent(BaseAgent):
    def __init__(self, player_profile: AthleteProfile, **kwargs):
        name = "Dr. Emily Carter - Sports Nutritionist"
        pp = player_profile.get_player_profile()  # Abbreviate dictionary access
        role = f"""
            You are a {pp['primary_sport']} Sports Nutrition Agent who also knows about {pp['secondary_sport']} specializing in optimizing athlete performance through diet.
            Your role is to **analyze player-specific data** and design **customized meal plans** 
            that enhance energy, endurance, recovery, and overall health.
            """
    
        goal = f"""
            Analyze the player profile of {pp['athlete_name']}. They are a {pp['athlete_age']} year old {pp['sex']}.
            They have a unique aspect of {pp['unique_aspect']} whose primary sport is {pp['primary_sport']} and 
                whose secondary sport is {pp['secondary_sport']}.

            Develop a **personalized nutrition strategy** based on the athlete’s profile.  
            Ensure the meal plan aligns with their **training intensity, recovery needs, and performance goals**.  
            Recommend **specific macronutrient and micronutrient intake** to maximize their athletic output.
            """

        backstory = """
            You are a highly experienced nutritionist who has worked with elite athletes 
            across multiple sports. You **understand the science of sports nutrition**, recovery, and meal 
            timing to ensure peak performance.
            """

        super().__init__(
            name=kwargs.pop('name', name),
            role=kwargs.pop('role', role),
            goal=kwargs.pop('goal', goal),
            backstory=kwargs.pop('backstory', backstory),
            **kwargs
        )

        self.player_profile = player_profile


    def generate_meal_plan(self):
        return crewai.Task(
            description=dedent(f"""
                Read the following player profile and create a **customized 1-month meal plan**:
                            {self.player_profile.get_player_profile()}

                Use knowledge in the Crew's context

                The meal plan should:
                - Be **tailored to the athlete’s specific training** and performance needs.
                - Include **high-protein meals** for muscle recovery.
                - Optimize **carbohydrate intake** for energy levels.
                - Balance **fats, vitamins, and hydration** for overall health.
                - Incorporate **pre-game and post-game nutrition strategies**.
                - Recommend **meal timing and portion sizes**.

                Ensure the plan is aligned with the athlete's age and **enhances endurance, strength, and recovery**, while preventing fatigue and injury.
            """),
            agent=self,
            expected_output="An age-appropriate structured 1-month meal plan designed to optimize the athlete’s performance."
        )
