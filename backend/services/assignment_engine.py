"""Ticket Assignment Engine - intelligent ticket assignment"""
from typing import Optional, Dict, List


class TicketAssignmentEngine:
    """Handles intelligent assignment of tickets to agents"""
    
    def __init__(self, db, user_service, analytics_service):
        self.db = db
        self.user_service = user_service
        self.analytics_service = analytics_service
        
    def assign_agent(self, ticket: Dict) -> Optional[str]:
        """
        Assign a ticket to the best available agent
        Considers: workload, past performance, sentiment
        """
        try:
            agents = self.user_service.get_agents()
            if not agents:
                return None
            
            agent_scores = {}
            for agent in agents:
                score = self._calculate_agent_score(agent, ticket)
                agent_scores[agent['user_id']] = score
            
            # Return agent with highest score
            best_agent = max(agent_scores.items(), key=lambda x: x[1])
            return best_agent[0]
        except Exception as e:
            return agents[0]['user_id'] if agents else None
    
    def _calculate_agent_score(self, agent: Dict, ticket: Dict) -> float:
        """Calculate assignment score for an agent"""
        score = 100.0
        
        # Get agent performance
        perf = self.analytics_service.get_agent_performance(agent['user_id'])
        
        # Reduce score based on workload (tickets assigned)
        workload = perf.get('total_assigned_tickets', 0)
        score -= workload * 2
        
        # Boost score based on customer satisfaction
        satisfaction = perf.get('customer_satisfaction_score', 0)
        score += satisfaction * 10
        
        # Adjust based on ticket priority
        priority = ticket.get('priority', 'medium')
        if priority == 'urgent':
            score += 20
        elif priority == 'high':
            score += 10
        
        return max(score, 0)
    
    def can_handle_ticket(self, agent_id: str, ticket_priority: str) -> bool:
        """Check if agent can handle a ticket with given priority"""
        perf = self.analytics_service.get_agent_performance(agent_id)
        workload = perf.get('total_assigned_tickets', 0)
        
        # Simple rule: max 10 tickets per agent
        return workload < 10
