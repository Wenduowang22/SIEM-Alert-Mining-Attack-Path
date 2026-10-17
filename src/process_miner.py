"""
Process mining module
DFG discovery, process tree induction, Petri net evaluation
Core logic from dissertation: Section 3.3 Process Mining Methods
"""
import pm4py
import pandas as pd

class AttackProcessMiner:
    def __init__(self):
        self.formatted_df = None
        self.event_log = None
        self.dfg = None
        self.start_activities = None
        self.end_activities = None

    def format_event_log(self, event_log_df: pd.DataFrame):
        """
        Convert DataFrame to PM4Py standard event log format
        Corresponds to dissertation: PM4Py Event Log Conversion
        """
        self.formatted_df = pm4py.format_dataframe(
            event_log_df,
            case_id="case_id",
            activity_key="activity",
            timestamp_key="timestamp",
        )
        self.event_log = pm4py.convert_to_event_log(self.formatted_df)
        return self.event_log

    def discover_dfg(self):
        """
        Discover Directly-Follows Graph
        Corresponds to dissertation: Directly-Follows Graph Discovery
        """
        self.dfg, self.start_activities, self.end_activities = pm4py.discover_dfg(self.formatted_df)
        return self.dfg, self.start_activities, self.end_activities

    def get_cross_activity_edges(self, top_n: int = 30) -> pd.DataFrame:
        """Get top N cross-activity transition relationships (filter out self-loops)"""
        if self.dfg is None:
            self.discover_dfg()
        
        edges = pd.DataFrame([
            {"source_activity": source, "target_activity": target, "frequency": int(freq)}
            for (source, target), freq in self.dfg.items()
        ])
        # Remove same-activity self-loops, keep cross-activity transitions only
        cross_edges = edges[edges["source_activity"] != edges["target_activity"]]
        return cross_edges.sort_values("frequency", ascending=False).head(top_n)

    def discover_process_tree(self, noise_threshold: float = 0.2):
        """
        Discover process tree using inductive miner
        Corresponds to dissertation: Inductive Miner process discovery
        """
        return pm4py.discover_process_tree_inductive(
            self.formatted_df, noise_threshold=noise_threshold
        )

    def evaluate_model(self, noise_threshold: float = 0.2) -> dict:
        """
        Evaluate model fitness and precision using token-based replay
        Corresponds to dissertation: Process Model Evaluation
        """
        process_tree = self.discover_process_tree(noise_threshold)
        net, im, fm = pm4py.convert_to_petri_net(process_tree)
        
        fitness = pm4py.fitness_token_based_replay(self.formatted_df, net, im, fm)
        precision = pm4py.precision_token_based_replay(self.formatted_df, net, im, fm)
        
        return {
            "noise_threshold": noise_threshold,
            "log_fitness": fitness.get("log_fitness"),
            "percentage_of_fitting_traces": fitness.get("percentage_of_fitting_traces"),
            "precision": float(precision),
            "places": len(net.places),
            "transitions": len(net.transitions),
            "arcs": len(net.arcs)
        }

