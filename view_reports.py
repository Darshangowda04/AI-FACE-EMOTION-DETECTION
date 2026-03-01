"""
Beautiful Report Viewer
Open and display emotion analysis reports in your browser
"""

import os
import webbrowser
import json
from pathlib import Path


class ReportViewer:
    """View and manage emotion analysis reports"""
    
    REPORT_DIR = Path.cwd()
    
    @staticmethod
    def list_reports():
        """List all available reports"""
        print("\n" + "=" * 70)
        print(" " * 20 + "AVAILABLE REPORTS")
        print("=" * 70 + "\n")
        
        html_reports = list(Path.cwd().glob("emotion_report_*.html"))
        png_reports = list(Path.cwd().glob("emotion_report_*.png"))
        json_reports = list(Path.cwd().glob("expression_analysis_*.json"))
        
        if not (html_reports or png_reports or json_reports):
            print("No reports found. Run analyze_expression.py first!")
            print("\nExample:\n  python analyze_expression.py --duration 15\n")
            return None
        
        print("📊 VISUAL REPORTS (PNG)")
        print("-" * 70)
        for i, report in enumerate(sorted(png_reports, reverse=True)[:10], 1):
            size = report.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"{i}. {report.name} ({size:.2f} MB)")
        
        print("\n🌐 WEB REPORTS (HTML)")
        print("-" * 70)
        for i, report in enumerate(sorted(html_reports, reverse=True)[:10], 1):
            size = report.stat().st_size / (1024)  # Size in KB
            print(f"{i}. {report.name} ({size:.1f} KB)")
        
        print("\n📁 DATA REPORTS (JSON)")
        print("-" * 70)
        for i, report in enumerate(sorted(json_reports, reverse=True)[:10], 1):
            size = report.stat().st_size / (1024)  # Size in KB
            print(f"{i}. {report.name} ({size:.1f} KB)")
        
        print("\n" + "=" * 70 + "\n")
        
        return {
            "html": html_reports,
            "png": png_reports,
            "json": json_reports
        }
    
    @staticmethod
    def open_latest_html_report():
        """Open the latest HTML report in browser"""
        html_reports = list(Path.cwd().glob("emotion_report_*.html"))
        
        if not html_reports:
            print("❌ No HTML reports found!")
            print("Run: python analyze_expression.py --duration 15")
            return False
        
        latest_report = sorted(html_reports, reverse=True)[0]
        
        print(f"\n🌐 Opening: {latest_report.name}")
        webbrowser.open('file://' + str(latest_report.absolute()))
        print("✅ Report opened in your default browser!")
        
        return True
    
    @staticmethod
    def open_latest_json_report():
        """Display the latest JSON report in terminal"""
        json_reports = list(Path.cwd().glob("expression_analysis_*.json"))
        
        if not json_reports:
            print("❌ No JSON reports found!")
            return False
        
        latest_report = sorted(json_reports, reverse=True)[0]
        
        with open(latest_report, 'r') as f:
            data = json.load(f)
        
        print("\n" + "=" * 70)
        print(" " * 15 + "DETAILED EMOTION ANALYSIS DATA")
        print("=" * 70)
        
        print(f"\n📅 Timestamp: {data['analysis_timestamp']}")
        print(f"⏱️  Duration: {data['duration']:.1f} seconds")
        print(f"📊 Total Frames: {data['total_frames']}")
        print(f"\n📈 Average Emotion Scores:")
        
        for emotion, score in sorted(data['average_emotion_scores'].items(), 
                                    key=lambda x: x[1], reverse=True):
            bar_length = int(score / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  {emotion.upper():10s} {bar} {score:6.2f}%")
        
        print("\n" + "=" * 70 + "\n")
        
        return True
    
    @staticmethod
    def clean_old_reports(keep_count: int = 5):
        """Keep only the latest N reports"""
        html_reports = sorted(Path.cwd().glob("emotion_report_*.html"), reverse=True)
        png_reports = sorted(Path.cwd().glob("emotion_report_*.png"), reverse=True)
        json_reports = sorted(Path.cwd().glob("expression_analysis_*.json"), reverse=True)
        
        deleted_count = 0
        
        # Clean HTML reports
        for report in html_reports[keep_count:]:
            report.unlink()
            deleted_count += 1
            print(f"🗑️  Deleted: {report.name}")
        
        # Clean PNG reports
        for report in png_reports[keep_count:]:
            report.unlink()
            deleted_count += 1
            print(f"🗑️  Deleted: {report.name}")
        
        # Clean JSON reports
        for report in json_reports[keep_count:]:
            report.unlink()
            deleted_count += 1
            print(f"🗑️  Deleted: {report.name}")
        
        if deleted_count == 0:
            print("No old reports to delete")
        else:
            print(f"\n✅ Deleted {deleted_count} old report(s)")


def main():
    """Main menu"""
    import argparse
    
    parser = argparse.ArgumentParser(description="View emotion analysis reports")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available reports"
    )
    parser.add_argument(
        "--open-html",
        action="store_true",
        help="Open latest HTML report in browser"
    )
    parser.add_argument(
        "--open-json",
        action="store_true",
        help="Display latest JSON report"
    )
    parser.add_argument(
        "--clean",
        type=int,
        metavar="N",
        help="Keep only latest N reports (default: 5)"
    )
    
    args = parser.parse_args()
    
    viewer = ReportViewer()
    
    if args.list:
        viewer.list_reports()
    elif args.open_html:
        viewer.open_latest_html_report()
    elif args.open_json:
        viewer.open_latest_json_report()
    elif args.clean:
        viewer.clean_old_reports(args.clean)
    else:
        # Show interactive menu
        print("\n" + "=" * 70)
        print(" " * 15 + "EMOTION ANALYSIS REPORT VIEWER")
        print("=" * 70)
        print("\nOptions:")
        print("  1. List all reports")
        print("  2. Open latest HTML report (in browser)")
        print("  3. Display latest JSON report")
        print("  4. Clean old reports")
        print("  5. Exit\n")
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            viewer.list_reports()
        elif choice == "2":
            viewer.open_latest_html_report()
        elif choice == "3":
            viewer.open_latest_json_report()
        elif choice == "4":
            count = input("Keep how many reports? (default: 5): ").strip()
            keep = int(count) if count.isdigit() else 5
            viewer.clean_old_reports(keep)
        elif choice == "5":
            print("Goodbye!")


if __name__ == "__main__":
    main()
