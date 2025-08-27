import reporter_agent
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a report based on a city and topic.")
    parser.add_argument("city", help="The name of the city for the report (e.g., 'New York')")
    parser.add_argument("topic", help="The topic for the report ('weather', 'news', or 'events')")
    args = parser.parse_args()
    city = args.city
    topic = args.topic
    try:
        agent = reporter_agent.ReporterAgent(city, topic)
        report_data = agent.get_data()
        report = agent.generate_report(report_data)
        agent.save_report(report)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()