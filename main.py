from dotenv import load_dotenv
from src.ui.interface import ColoringSheetInterface
from src.crews.coloring_sheet_crew import ColoringSheetCrew

def main():
    load_dotenv()
    ai_crew = ColoringSheetCrew()  # Create the crew instance directly
    interface = ColoringSheetInterface(ai_crew)
    interface.launch()

if __name__ == "__main__":
    main()
