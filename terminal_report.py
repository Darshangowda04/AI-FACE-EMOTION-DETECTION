"""
Beautiful Terminal Report Generator
Displays emotion analysis reports in the terminal with colors and formatting
"""

import sys
from datetime import datetime


class Colors:
    """ANSI color codes for terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'
    PURPLE = '\033[35m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Emotion colors
    HAPPY = GREEN
    CALM = BLUE
    NEUTRAL = GRAY
    FOCUS = ORANGE
    INTENSE = RED


class TerminalReport:
    """Generate beautiful terminal reports for emotion analysis"""
    
    def __init__(self, emotion_data, detector):
        """Initialize terminal report"""
        self.emotion_data = emotion_data
        self.detector = detector
        self.emotion_counts = self._calculate_emotion_counts()
        self.avg_scores = self._calculate_avg_scores()
    
    def _calculate_emotion_counts(self):
        """Calculate emotion frequencies"""
        counts = {}
        for data in self.emotion_data:
            emotion = data["emotion"]
            counts[emotion] = counts.get(emotion, 0) + 1
        return counts
    
    def _calculate_avg_scores(self):
        """Calculate average scores for each emotion"""
        scores = {e: 0 for e in self.detector.ALL_EMOTIONS}
        for data in self.emotion_data:
            emotions = data.get("all_emotions", {})
            for emotion in self.detector.ALL_EMOTIONS:
                scores[emotion] += emotions.get(emotion, 0)
        
        for emotion in scores:
            scores[emotion] /= len(self.emotion_data) if self.emotion_data else 1
        
        return scores
    
    def print_header(self):
        """Print report header"""
        print("\n")
        print(Colors.CYAN + "=" * 80 + Colors.END)
        print(Colors.CYAN + " " * 15 + Colors.BOLD + "🎭 EMOTION ANALYSIS REPORT 🎭" + Colors.END)
        print(Colors.CYAN + "=" * 80 + Colors.END)
        print(f"{Colors.GRAY}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print()
    
    def print_statistics(self):
        """Print overall statistics"""
        confidences = [d["confidence"] for d in self.emotion_data]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        print(Colors.BOLD + Colors.CYAN + "\n📊 OVERALL STATISTICS" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        print(f"{Colors.WHITE}Total Frames Analyzed:{Colors.END} {Colors.YELLOW}{len(self.emotion_data)}{Colors.END}")
        print(f"{Colors.WHITE}Duration:{Colors.END} {Colors.YELLOW}{self.emotion_data[-1]['timestamp']:.1f}{Colors.END} seconds")
        print(f"{Colors.WHITE}Frames Per Second:{Colors.END} {Colors.YELLOW}{len(self.emotion_data) / self.emotion_data[-1]['timestamp']:.1f}{Colors.END} FPS")
        print(f"{Colors.WHITE}Faces Detected:{Colors.END} {Colors.YELLOW}{self.emotion_data[0].get('faces_detected', 1)}{Colors.END}")
        print(f"{Colors.WHITE}Average Confidence:{Colors.END} {Colors.YELLOW}{avg_confidence:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}Max Confidence:{Colors.END} {Colors.YELLOW}{max(confidences)}%{Colors.END}")
        print(f"{Colors.WHITE}Min Confidence:{Colors.END} {Colors.YELLOW}{min(confidences)}%{Colors.END}")
    
    def print_dominant_emotions(self):
        """Print dominant emotions"""
        print(Colors.BOLD + Colors.GREEN + "\n😊 DOMINANT EMOTIONS" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        sorted_emotions = sorted(self.emotion_counts.items(), key=lambda x: x[1], reverse=True)
        
        for emotion, count in sorted_emotions:
            percentage = (count / len(self.emotion_data)) * 100
            bar_length = int(percentage / 2.5)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            
            emotion_color = self._get_emotion_color(emotion)
            emoji = self._get_emotion_emoji(emotion)
            
            print(f"{emotion_color}{emoji} {emotion.upper():10s}{Colors.END} {bar} {Colors.YELLOW}{percentage:5.1f}%{Colors.END} ({count} frames)")
    
    def print_confidence_analysis(self):
        """Print confidence analysis"""
        confidences = [d["confidence"] for d in self.emotion_data]
        avg_confidence = sum(confidences) / len(confidences)
        max_confidence = max(confidences)
        min_confidence = min(confidences)
        
        stability = "High" if avg_confidence > 70 else "Moderate" if avg_confidence > 50 else "Low"
        stability_color = Colors.GREEN if stability == "High" else Colors.YELLOW if stability == "Moderate" else Colors.RED
        
        print(Colors.BOLD + Colors.YELLOW + "\n🎯 CONFIDENCE ANALYSIS" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        print(f"{Colors.WHITE}Average Confidence:{Colors.END} {Colors.YELLOW}{avg_confidence:.1f}%{Colors.END}")
        print(f"{Colors.WHITE}Maximum Confidence:{Colors.END} {Colors.YELLOW}{max_confidence}%{Colors.END}")
        print(f"{Colors.WHITE}Minimum Confidence:{Colors.END} {Colors.YELLOW}{min_confidence}%{Colors.END}")
        print(f"{Colors.WHITE}Confidence Stability:{Colors.END} {stability_color}{stability}{Colors.END}")
    
    def print_detailed_emotion_scores(self):
        """Print detailed emotion breakdown"""
        print(Colors.BOLD + Colors.PURPLE + "\n📈 DETAILED EMOTION BREAKDOWN" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        sorted_scores = sorted(self.avg_scores.items(), key=lambda x: x[1], reverse=True)
        
        for emotion, score in sorted_scores:
            bar_length = int(score / 2.5)
            bar = "█" * bar_length + "░" * (40 - bar_length)
            
            emotion_color = self._get_emotion_color(emotion)
            emoji = self._get_emotion_emoji(emotion)
            
            print(f"{emotion_color}{emoji} {emotion.upper():10s}{Colors.END} {bar} {Colors.YELLOW}{score:6.2f}%{Colors.END}")
    
    def print_emotion_transitions(self):
        """Print emotion transitions"""
        transitions = []
        for i in range(1, len(self.emotion_data)):
            if self.emotion_data[i]["emotion"] != self.emotion_data[i-1]["emotion"]:
                transitions.append({
                    "from": self.emotion_data[i-1]["emotion"],
                    "to": self.emotion_data[i]["emotion"],
                    "time": self.emotion_data[i]["timestamp"]
                })
        
        print(Colors.BOLD + Colors.BLUE + "\n🔄 EMOTION TRANSITIONS" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        if not transitions:
            print(f"{Colors.GREEN}✓ No transitions detected{Colors.END} - Consistent expression throughout!")
        else:
            print(f"Total emotion changes: {Colors.YELLOW}{len(transitions)}{Colors.END}\n")
            
            # Show first 10 transitions
            for j, transition in enumerate(transitions[:10], 1):
                from_color = self._get_emotion_color(transition['from'])
                to_color = self._get_emotion_color(transition['to'])
                from_emoji = self._get_emotion_emoji(transition['from'])
                to_emoji = self._get_emotion_emoji(transition['to'])
                
                print(f"  {j}. {from_color}{from_emoji} {transition['from'].title()}{Colors.END} → {to_color}{to_emoji} {transition['to'].title()}{Colors.END} at {Colors.YELLOW}{transition['time']:.1f}s{Colors.END}")
            
            if len(transitions) > 10:
                print(f"  ... and {Colors.YELLOW}{len(transitions) - 10}{Colors.END} more transitions")
    
    def print_assessment(self):
        """Print assessment section"""
        dominant = max(self.emotion_counts, key=self.emotion_counts.get)
        avg_confidence = sum([d["confidence"] for d in self.emotion_data]) / len(self.emotion_data)
        transitions = self._count_transitions()
        
        assessment = self._generate_assessment(dominant, avg_confidence, transitions)
        
        print(Colors.BOLD + Colors.ORANGE + "\n📋 ASSESSMENT" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        print(assessment)
    
    def print_developer_credits(self):
        """Print developer credits"""
        print(Colors.BOLD + Colors.YELLOW + "\n👨‍💻 DEVELOPED BY" + Colors.END)
        print(Colors.CYAN + "-" * 80 + Colors.END)
        
        print(f"{Colors.BOLD}{Colors.WHITE}DARSHAN GOWDA G D{Colors.END}")
        print()
        print(f"{Colors.BOLD}GitHub:{Colors.END}")
        print(f"  {Colors.CYAN}https://github.com/Darshangowda04{Colors.END}")
        print()
        print(f"{Colors.BOLD}LinkedIn:{Colors.END}")
        print(f"  {Colors.CYAN}https://www.linkedin.com/in/darshan-gowda-g-d-b7473132b/{Colors.END}")
        print()
        print(f"{Colors.GRAY}© 2026 - All Rights Reserved{Colors.END}")
    
    def print_footer(self):
        """Print report footer"""
        print()
        print(Colors.CYAN + "=" * 80 + Colors.END)
        print(f"{Colors.GREEN}✅ Report generated successfully!{Colors.END}")
        print(Colors.CYAN + "=" * 80 + Colors.END)
        print()
    
    def _get_emotion_color(self, emotion: str):
        """Get color for emotion"""
        color_map = {
            "happy": Colors.HAPPY,
            "calm": Colors.CALM,
            "neutral": Colors.NEUTRAL,
            "focus": Colors.FOCUS,
            "intense": Colors.INTENSE
        }
        return color_map.get(emotion, Colors.WHITE)
    
    def _get_emotion_emoji(self, emotion: str) -> str:
        """Get emoji for emotion"""
        emoji_map = {
            "happy": "😊",
            "calm": "😌",
            "neutral": "😐",
            "focus": "🧐",
            "intense": "😠"
        }
        return emoji_map.get(emotion, "😶")
    
    def _count_transitions(self) -> int:
        """Count emotion transitions"""
        transitions = 0
        for i in range(1, len(self.emotion_data)):
            if self.emotion_data[i]["emotion"] != self.emotion_data[i-1]["emotion"]:
                transitions += 1
        return transitions
    
    def _generate_assessment(self, dominant: str, avg_conf: float, transitions: int) -> str:
        """Generate assessment text"""
        
        emotion_map = {
            "happy": f"{Colors.GREEN}Your expression shows happiness and positivity!{Colors.END}",
            "calm": f"{Colors.BLUE}Your expression is calm and composed. You appear relaxed.{Colors.END}",
            "neutral": f"{Colors.GRAY}Your expression is neutral and balanced.{Colors.END}",
            "focus": f"{Colors.ORANGE}Your expression shows focus and concentration. You seem engaged.{Colors.END}",
            "intense": f"{Colors.RED}Your expression is intense or expressive.{Colors.END}"
        }
        
        emoji_map = {
            "happy": "😊",
            "calm": "😌",
            "neutral": "😐",
            "focus": "🧐",
            "intense": "😠"
        }
        
        emoji = emoji_map.get(dominant, "😶")
        emotion_text = emotion_map.get(dominant, "Mixed emotions detected")
        
        # Confidence assessment
        if avg_conf > 80:
            confidence_text = f"Your expression was {Colors.GREEN}very clear and consistent{Colors.END} throughout the analysis."
        elif avg_conf > 60:
            confidence_text = f"Your expression was {Colors.YELLOW}clear with slight variations{Colors.END} in intensity."
        else:
            confidence_text = f"Your expression {Colors.YELLOW}varied quite a bit{Colors.END} during the analysis."
        
        # Transition assessment
        if transitions == 0:
            transition_text = f"You {Colors.GREEN}maintained a stable expression{Colors.END} throughout the entire session."
        elif transitions <= 2:
            transition_text = f"Your expression remained {Colors.GREEN}mostly stable{Colors.END} with minimal changes."
        else:
            transition_text = f"Your expression changed {Colors.YELLOW}{transitions} times{Colors.END}, showing emotional variety."
        
        return f"{emoji} {emotion_text}\n{confidence_text}\n{transition_text}"
    
    def generate(self):
        """Generate complete terminal report"""
        self.print_header()
        self.print_statistics()
        self.print_dominant_emotions()
        self.print_confidence_analysis()
        self.print_detailed_emotion_scores()
        self.print_emotion_transitions()
        self.print_assessment()
        self.print_developer_credits()
        self.print_footer()


def print_terminal_report(emotion_data, detector):
    """Display terminal report"""
    report = TerminalReport(emotion_data, detector)
    report.generate()
