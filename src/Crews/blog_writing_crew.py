import crewai as crewai
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

import logging

from src.Agents.blog_post_agents import BlogWriterAgent, BlogCriticAgent, BlogTopicAgent, BlogValidationAgent, BlogPublisherAgent
from src.Models.llm_config import gpt_4o_llm_random
import src.Agents.agent_helpers as agent_helpers
import src.Utils.utils as utils


class BlogWritingCrew:
    def run(self):
        logger = utils.configure_logger(logging.INFO)

        blog_topic_agent  = BlogTopicAgent(llm=gpt_4o_llm_random)
        blog_writer_agent = BlogWriterAgent(llm=gpt_4o_llm_random)
        blog_critic_agent = BlogCriticAgent(llm=gpt_4o_llm_random)
        blog_validation_agent = BlogValidationAgent(llm=gpt_4o_llm_random)
        blog_publisher_agent = BlogPublisherAgent(llm=gpt_4o_llm_random)
        
        agents = [
            blog_topic_agent,
            blog_writer_agent,
            blog_critic_agent,
            blog_validation_agent,
            blog_publisher_agent
        ]

        tasks = [
            blog_topic_agent.select_blog_topic(),
            blog_writer_agent.write_blog_post(),
            blog_critic_agent.critique_blog_post(),
            blog_writer_agent.revise_blog_post(),
            blog_validation_agent.validate_blog_post(),
            blog_publisher_agent.publish_blog_post()
        ]
        

        # Run tasks
        crew = crewai.Crew(
            agents=agents,
            tasks=tasks,
            process=crewai.Process.sequential,
            verbose=True
        )

        # Register crew with BaseAgent        
        for agent in crew.agents:
            logger.info(f"Agent Name: '{agent.role}'")
            agent.register_crew(crew)

        result = crew.kickoff()
        return result
