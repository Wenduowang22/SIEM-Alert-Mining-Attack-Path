"""
Model evaluation module
False positive reduction rate, noise reduction metrics and model quality summary
Core logic from dissertation: Section 4.4 Model Quality & Evaluation
"""

class ModelEvaluator:
    def __init__(self):
        pass

    def calculate_fp_reduction(self, original_alerts: int, true_attack_cases: int) -> dict:
        """
        Calculate false positive reduction effect
        Based on dissertation: 1.6M raw alerts → 1692 true attack cases
        """
        reduction_rate = (original_alerts - true_attack_cases) / original_alerts
        return {
            "original_alert_count": original_alerts,
            "true_attack_cases": true_attack_cases,
            "false_positive_reduction_rate": f"{round(reduction_rate * 100, 2)}%",
            "noise_reduction_factor": round(original_alerts / true_attack_cases, 1)
        }

    def get_full_summary(self, data_processor) -> dict:
        """Generate full project effect metrics for API response"""
        metrics = data_processor.get_basic_metrics()
        # Full dataset baseline: ~1.6M raw alerts (consistent with dissertation)
        fp_metrics = self.calculate_fp_reduction(1600000, metrics["number_of_cases"])
        
        return {
            **metrics,
            **fp_metrics,
            "dataset": "Microsoft GUIDE Security Alert Dataset"
        }

