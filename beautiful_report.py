"""
Beautiful Visual Report Generator
Creates stunning colored reports with charts and developer credits
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime
from pathlib import Path


class BeautifulReportGenerator:
    """Generate beautiful visual reports for emotion analysis"""
    
    # Developer Info
    DEVELOPER_NAME = "DARSHAN GOWDA G D"
    GITHUB_URL = "https://github.com/Darshangowda04"
    LINKEDIN_URL = "https://www.linkedin.com/in/darshan-gowda-g-d-b7473132b/"
    
    # Color scheme
    COLORS = {
        "happy": "#2ECC71",      # Green
        "calm": "#3498DB",       # Blue
        "neutral": "#95A5A6",    # Gray
        "focus": "#F39C12",      # Orange
        "intense": "#E74C3C"     # Red
    }
    
    BACKGROUND = "#1A1A2E"
    ACCENT = "#16213E"
    TEXT = "#FFFFFF"
    
    def __init__(self, emotion_data, detector):
        """Initialize report generator"""
        self.emotion_data = emotion_data
        self.detector = detector
        self.fig = None
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
    
    def generate_full_report(self, filename: str = None) -> str:
        """Generate complete beautiful report with all charts"""
        
        if filename is None:
            filename = f"emotion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Create figure with subplots
        self.fig = plt.figure(figsize=(20, 14), facecolor=self.BACKGROUND)
        self.fig.suptitle(
            "EMOTION ANALYSIS REPORT",
            fontsize=28,
            fontweight='bold',
            color=self.TEXT,
            y=0.98
        )
        
        # Create grid for subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3, 
                                    left=0.08, right=0.95, top=0.94, bottom=0.08)
        
        # 1. Pie chart of dominant emotions
        ax1 = self.fig.add_subplot(gs[0, 0])
        self._draw_emotion_pie(ax1)
        
        # 2. Emotion timeline
        ax2 = self.fig.add_subplot(gs[0, 1:])
        self._draw_emotion_timeline(ax2)
        
        # 3. Bar chart of average scores
        ax3 = self.fig.add_subplot(gs[1, 0])
        self._draw_emotion_bars(ax3)
        
        # 4. Confidence metrics
        ax4 = self.fig.add_subplot(gs[1, 1])
        self._draw_confidence_gauge(ax4)
        
        # 5. Statistics box
        ax5 = self.fig.add_subplot(gs[1, 2])
        self._draw_statistics_box(ax5)
        
        # 6. Assessment text
        ax6 = self.fig.add_subplot(gs[2, :2])
        self._draw_assessment(ax6)
        
        # 7. Developer credits
        ax7 = self.fig.add_subplot(gs[2, 2])
        self._draw_developer_credits(ax7)
        
        # Save figure
        plt.savefig(filename, dpi=300, facecolor=self.BACKGROUND, 
                   edgecolor='none', bbox_inches='tight')
        print(f"📊 Visual report saved: {filename}")
        plt.close()
        
        return filename
    
    def _draw_emotion_pie(self, ax):
        """Draw pie chart of dominant emotions"""
        emotions = list(self.emotion_counts.keys())
        counts = list(self.emotion_counts.values())
        colors = [self.COLORS.get(e, "#95A5A6") for e in emotions]
        
        wedges, texts, autotexts = ax.pie(
            counts,
            labels=emotions,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10, 'color': self.TEXT, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title("Emotion Distribution", color=self.TEXT, fontsize=12, 
                    fontweight='bold', pad=10)
        ax.set_facecolor(self.ACCENT)
    
    def _draw_emotion_timeline(self, ax):
        """Draw emotion changes over time"""
        times = [d["timestamp"] for d in self.emotion_data]
        emotions = [d["emotion"] for d in self.emotion_data]
        
        # Create color array for timeline
        emotion_to_num = {e: i for i, e in enumerate(self.detector.ALL_EMOTIONS)}
        emotion_nums = [emotion_to_num.get(e, 0) for e in emotions]
        
        # Create color map
        color_map = [self.COLORS.get(e, "#95A5A6") for e in emotions]
        
        # Plot timeline
        for i in range(len(times) - 1):
            ax.plot(times[i:i+2], [emotion_nums[i], emotion_nums[i+1]], 
                   color=color_map[i], linewidth=3, marker='o', markersize=4)
        
        ax.set_xlabel("Time (seconds)", color=self.TEXT, fontsize=10, fontweight='bold')
        ax.set_ylabel("Emotion", color=self.TEXT, fontsize=10, fontweight='bold')
        ax.set_yticks(range(len(self.detector.ALL_EMOTIONS)))
        ax.set_yticklabels(self.detector.ALL_EMOTIONS, color=self.TEXT)
        ax.set_facecolor(self.ACCENT)
        ax.grid(True, alpha=0.2, color=self.TEXT)
        
        # Style axes
        ax.spines['bottom'].set_color(self.TEXT)
        ax.spines['left'].set_color(self.TEXT)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors=self.TEXT, labelsize=9)
        
        ax.set_title("Emotion Timeline", color=self.TEXT, fontsize=12, 
                    fontweight='bold', pad=10)
    
    def _draw_emotion_bars(self, ax):
        """Draw horizontal bar chart of average emotion scores"""
        emotions = list(self.avg_scores.keys())
        scores = [self.avg_scores[e] for e in emotions]
        colors = [self.COLORS.get(e, "#95A5A6") for e in emotions]
        
        # Sort by score
        sorted_data = sorted(zip(emotions, scores, colors), key=lambda x: x[1], reverse=True)
        emotions_sorted, scores_sorted, colors_sorted = zip(*sorted_data)
        
        bars = ax.barh(emotions_sorted, scores_sorted, color=colors_sorted, edgecolor=self.TEXT, linewidth=1.5)
        
        # Add score labels
        for i, (bar, score) in enumerate(zip(bars, scores_sorted)):
            ax.text(score + 1, i, f'{score:.1f}%', va='center', color=self.TEXT, 
                   fontweight='bold', fontsize=9)
        
        ax.set_xlabel("Average Score (%)", color=self.TEXT, fontsize=10, fontweight='bold')
        ax.set_xlim(0, 100)
        ax.set_facecolor(self.ACCENT)
        ax.grid(True, alpha=0.2, axis='x', color=self.TEXT)
        
        # Style
        ax.spines['bottom'].set_color(self.TEXT)
        ax.spines['left'].set_color(self.TEXT)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors=self.TEXT, labelsize=9)
        
        ax.set_title("Average Emotion Scores", color=self.TEXT, fontsize=12, 
                    fontweight='bold', pad=10)
    
    def _draw_confidence_gauge(self, ax):
        """Draw confidence gauge"""
        avg_confidence = np.mean([d["confidence"] for d in self.emotion_data])
        
        # Draw gauge background
        ax.add_patch(patches.Wedge((0, 0), 1, 180, 360, 
                                   facecolor=self.ACCENT, edgecolor=self.TEXT, linewidth=2))
        
        # Draw confidence indicator
        angle = 180 + (avg_confidence / 100) * 180
        ax.arrow(0, 0, np.cos(np.radians(angle)), np.sin(np.radians(angle)), 
                head_width=0.1, head_length=0.1, fc='#FFD700', ec='#FFD700', linewidth=2)
        
        # Add labels
        ax.text(0, -0.7, f'{avg_confidence:.0f}%', ha='center', fontsize=20, 
               color=self.TEXT, fontweight='bold')
        ax.text(0, -0.9, 'Confidence', ha='center', fontsize=10, color=self.TEXT)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Background
        ax.set_facecolor(self.ACCENT)
    
    def _draw_statistics_box(self, ax):
        """Draw statistics box"""
        stats_text = f"""
STATISTICS

Total Frames: {len(self.emotion_data)}
Duration: {self.emotion_data[-1]['timestamp']:.1f}s
FPS: {len(self.emotion_data) / self.emotion_data[-1]['timestamp']:.1f}
Faces: {self.emotion_data[0].get('faces_detected', 1)}

Dominant: {max(self.emotion_counts, key=self.emotion_counts.get).upper()}
Confidence: {np.mean([d['confidence'] for d in self.emotion_data]):.1f}%

Transitions: {self._count_transitions()}
        """
        
        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', color=self.TEXT,
               family='monospace', fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=self.ACCENT, edgecolor=self.TEXT, linewidth=2))
        
        ax.axis('off')
        ax.set_facecolor(self.BACKGROUND)
    
    def _draw_assessment(self, ax):
        """Draw assessment text"""
        dominant = max(self.emotion_counts, key=self.emotion_counts.get)
        avg_conf = np.mean([d["confidence"] for d in self.emotion_data])
        transitions = self._count_transitions()
        
        assessment = self._generate_assessment_text(dominant, avg_conf, transitions)
        
        ax.text(0.05, 0.95, assessment, transform=ax.transAxes,
               fontsize=11, verticalalignment='top', color=self.TEXT,
               fontweight='bold', wrap=True, family='sans-serif',
               bbox=dict(boxstyle='round,pad=1', facecolor=self.ACCENT, 
                        edgecolor=self.COLORS.get(dominant, "#95A5A6"), linewidth=3))
        
        ax.axis('off')
        ax.set_facecolor(self.BACKGROUND)
    
    def _draw_developer_credits(self, ax):
        """Draw developer credits with links"""
        credits_text = f"""
DEVELOPED BY

{self.DEVELOPER_NAME}

GitHub:
{self.GITHUB_URL}

LinkedIn:
{self.LINKEDIN_URL}

© 2026 - All Rights Reserved
        """
        
        ax.text(0.5, 0.5, credits_text, transform=ax.transAxes,
               fontsize=9, ha='center', va='center', color=self.TEXT,
               fontweight='bold', family='monospace',
               bbox=dict(boxstyle='round,pad=1', facecolor=self.ACCENT, 
                        edgecolor='#FFD700', linewidth=3))
        
        ax.axis('off')
        ax.set_facecolor(self.BACKGROUND)
    
    def _count_transitions(self) -> int:
        """Count emotion transitions"""
        transitions = 0
        for i in range(1, len(self.emotion_data)):
            if self.emotion_data[i]["emotion"] != self.emotion_data[i-1]["emotion"]:
                transitions += 1
        return transitions
    
    def _generate_assessment_text(self, dominant: str, avg_conf: float, transitions: int) -> str:
        """Generate assessment text"""
        
        emoji_map = {
            "happy": "😊",
            "calm": "😌",
            "neutral": "😐",
            "focus": "🧐",
            "intense": "😠"
        }
        
        emoji = emoji_map.get(dominant, "😶")
        
        assessment_map = {
            "happy": "Your expression shows happiness and positivity!",
            "calm": "Your expression is calm and composed.",
            "neutral": "Your expression is neutral and balanced.",
            "focus": "Your expression shows focus and concentration.",
            "intense": "Your expression is intense and expressive."
        }
        
        main_assessment = assessment_map.get(dominant, "Mixed emotions detected")
        
        if transitions == 0:
            transition_text = "You maintained a stable expression throughout."
        elif transitions <= 2:
            transition_text = "Your expression remained mostly stable."
        else:
            transition_text = f"Your expression changed {transitions} times."
        
        return f"{emoji} {main_assessment}\n{transition_text}\nConfidence: {avg_conf:.0f}%"
    
    def generate_html_report(self, filename: str = None) -> str:
        """Generate beautiful HTML report"""
        
        if filename is None:
            filename = f"emotion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        dominant_emotion = max(self.emotion_counts, key=self.emotion_counts.get)
        avg_confidence = np.mean([d["confidence"] for d in self.emotion_data])
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Analysis Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(22, 33, 62, 0.8);
            border-radius: 15px;
            border: 2px solid #00d4ff;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }}
        
        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            color: #00d4ff;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }}
        
        .timestamp {{
            color: #a0a0a0;
            font-size: 0.9em;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .card {{
            background: rgba(22, 33, 62, 0.9);
            border-radius: 12px;
            padding: 25px;
            border: 2px solid #00d4ff;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
        }}
        
        .card h2 {{
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }}
        
        .stat {{
            display: flex;
            justify-content: space-between;
            margin: 12px 0;
            padding: 10px;
            background: rgba(0, 212, 255, 0.05);
            border-radius: 8px;
        }}
        
        .stat-value {{
            color: #00d4ff;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .emotion-bar {{
            display: flex;
            align-items: center;
            margin: 15px 0;
            gap: 10px;
        }}
        
        .emotion-name {{
            width: 100px;
            font-weight: bold;
        }}
        
        .bar-container {{
            flex: 1;
            height: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .bar-fill {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            font-weight: bold;
            color: white;
            transition: width 0.3s ease;
        }}
        
        .happy {{ background: linear-gradient(90deg, #2ECC71, #27AE60); }}
        .calm {{ background: linear-gradient(90deg, #3498DB, #2980B9); }}
        .neutral {{ background: linear-gradient(90deg, #95A5A6, #7F8C8D); }}
        .focus {{ background: linear-gradient(90deg, #F39C12, #E67E22); }}
        .intense {{ background: linear-gradient(90deg, #E74C3C, #C0392B); }}
        
        .assessment {{
            background: rgba(22, 33, 62, 0.9);
            border-radius: 12px;
            padding: 20px;
            border-left: 5px solid #00d4ff;
            margin: 20px 0;
            font-size: 1.1em;
            line-height: 1.6;
        }}
        
        .developer-section {{
            background: rgba(22, 33, 62, 0.9);
            border-radius: 12px;
            padding: 30px;
            border: 2px solid #FFD700;
            text-align: center;
            margin-top: 40px;
        }}
        
        .developer-section h3 {{
            color: #FFD700;
            font-size: 1.5em;
            margin-bottom: 15px;
        }}
        
        .developer-section p {{
            margin: 10px 0;
            font-size: 1.1em;
        }}
        
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .social-link {{
            color: #00d4ff;
            text-decoration: none;
            padding: 10px 20px;
            border: 2px solid #00d4ff;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .social-link:hover {{
            background: #00d4ff;
            color: #1a1a2e;
            font-weight: bold;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
        
        canvas {{
            max-height: 300px;
        }}
        
        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>😊 EMOTION ANALYSIS REPORT</h1>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="grid">
            <!-- Statistics Card -->
            <div class="card">
                <h2>📊 Statistics</h2>
                <div class="stat">
                    <span>Total Frames:</span>
                    <span class="stat-value">{len(self.emotion_data)}</span>
                </div>
                <div class="stat">
                    <span>Duration:</span>
                    <span class="stat-value">{self.emotion_data[-1]['timestamp']:.1f}s</span>
                </div>
                <div class="stat">
                    <span>FPS:</span>
                    <span class="stat-value">{len(self.emotion_data) / self.emotion_data[-1]['timestamp']:.1f}</span>
                </div>
                <div class="stat">
                    <span>Faces Detected:</span>
                    <span class="stat-value">{self.emotion_data[0].get('faces_detected', 1)}</span>
                </div>
                <div class="stat">
                    <span>Avg Confidence:</span>
                    <span class="stat-value">{avg_confidence:.1f}%</span>
                </div>
                <div class="stat">
                    <span>Dominant Emotion:</span>
                    <span class="stat-value">{dominant_emotion.upper()}</span>
                </div>
            </div>
            
            <!-- Emotion Distribution -->
            <div class="card">
                <h2>😊 Emotion Distribution</h2>
                {"".join([f'''
                <div class="emotion-bar">
                    <div class="emotion-name">{emotion.upper()}</div>
                    <div class="bar-container">
                        <div class="bar-fill {emotion}" style="width: {(count/len(self.emotion_data))*100}%">
                            {(count/len(self.emotion_data))*100:.1f}%
                        </div>
                    </div>
                </div>
                ''' for emotion, count in sorted(self.emotion_counts.items(), key=lambda x: x[1], reverse=True)])}
            </div>
            
            <!-- Detailed Scores -->
            <div class="card">
                <h2>📈 Detailed Scores</h2>
                {"".join([f'''
                <div class="emotion-bar">
                    <div class="emotion-name">{emotion.upper()}</div>
                    <div class="bar-container">
                        <div class="bar-fill {emotion}" style="width: {score}%">
                            {score:.1f}%
                        </div>
                    </div>
                </div>
                ''' for emotion, score in sorted(self.avg_scores.items(), key=lambda x: x[1], reverse=True)])}
            </div>
        </div>
        
        <!-- Assessment -->
        <div class="assessment">
            <strong>Assessment:</strong><br>
            Your expression shows <strong>{dominant_emotion.upper()}</strong> with an average confidence of <strong>{avg_confidence:.1f}%</strong>. 
            You had <strong>{self._count_transitions()} emotion transition(s)</strong> during the analysis.
        </div>
        
        <!-- Developer Section -->
        <div class="developer-section">
            <h3>👨‍💻 DEVELOPED BY</h3>
            <p><strong>{self.DEVELOPER_NAME}</strong></p>
            <p style="color: #a0a0a0; font-size: 0.9em;">AI Face Emotion Detection System</p>
            <div class="social-links">
                <a href="{self.GITHUB_URL}" class="social-link" target="_blank">🔗 GitHub</a>
                <a href="{self.LINKEDIN_URL}" class="social-link" target="_blank">🔗 LinkedIn</a>
            </div>
            <p style="margin-top: 20px; color: #a0a0a0; font-size: 0.8em;">© 2026 - All Rights Reserved</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 HTML report saved: {filename}")
        return filename
