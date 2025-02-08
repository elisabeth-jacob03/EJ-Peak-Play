import crewai as crewai
from textwrap import dedent
from src.Agents.base_agent import BaseAgent


class PhysiologyAgent(BaseAgent):
    def __init__(self, input_file: str, **kwargs):
        name = "Dr. Robert Lee - Physiology Specialist"
        role = """
            You are a Sports Physiologist specializing in optimizing athletic performance through 
            **exercise science, injury prevention, and recovery techniques**. Your role is to analyze 
            **player-specific data** and develop **tailored strategies** to improve endurance, strength, 
            and long-term physical health.
            """
    
        goal = """
            Use the athlete's **biometric and training data** to provide **personalized physiology advice**.  
            Ensure that all recommendations are **age-appropriate, sport-specific, and designed for  
            long-term development**.  
            Provide clear guidance on **injury prevention, muscle recovery, and performance optimization**.
            """

        backstory = """
            With deep expertise in **exercise physiology**, you have helped elite athletes refine  
            their physical conditioning and avoid injuries. Your approach is based on the latest  
            research in **sports science, biomechanics, and rehabilitation**.
            """

        super().__init__(
            name=kwargs.pop('name', name),
            input_file=input_file,
            role=kwargs.pop('role', role),
            goal=kwargs.pop('goal', goal),
            backstory=kwargs.pop('backstory', backstory),
            **kwargs
        )

    def generate_physiology_report(self):
        """ Reads the input file and generates a physiology report """
        player_data = self.read_input_file()  # Fetch player profile dynamically

        return crewai.Task(
            description=dedent(f"""
                Read the following player profile and provide **a physiology report**  
                with **specific recommendations** for **injury prevention, recovery, and physical optimization**.

                **Player Data:**
                {player_data}

                Your response should include:
                - **Injury prevention techniques** (specific to the athlete's sport)
                - **Recovery strategies** (nutrition, hydration, sleep, and muscle repair)
                - **Mobility and flexibility exercises** to prevent strains
                - **Cardiovascular endurance strategies** for long-lasting performance
                - **Strength-building recommendations** (safe and effective)

                Ensure that all recommendations are **scientifically backed** and **tailored to the athlete's physical condition**.
            """),
            agent=self,
            expected_output="A structured physiology report detailing injury prevention and performance enhancement strategies."
        )
