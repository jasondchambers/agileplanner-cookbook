from datetime import date
import agileplanner as ap

class HolidaySchedule(ap.HolidaySchedulePort):
    def __init__(self) -> None:
        self.holidays = {}
        self.holidays['US'] = [
            date(2023,1,2),
            date(2023,1,3), # DayForMe
            date(2023,1,16),
            date(2023,2,20), # DayForMe
            date(2023,5,29),
            date(2023,5,22), # DayForMe
            date(2023,6,19),
            date(2023,7,4),
            date(2023,9,4),
            date(2023,9,18), # DayForMe
            date(2023,11,10),
            date(2023,11,23),
            date(2023,11,24),
            date(2023,12,25),
            date(2023,12,26),
            date(2023,12,27), #shutdown
            date(2023,12,28), #shutdown
            date(2023,12,29), #shutdown
            date(2024,1,1),
            date(2024,1,2) # DayForMe
        ]
        self.holidays['Bangalore'] = [
            date(2023,1,26),
            date(2023,1,3), # DayForMe
            date(2023,2,20), # DayForMe
            date(2023,3,22),
            date(2023,4,7),
            date(2023,5,1),
            date(2023,5,22), # DayForMe
            date(2023,6,29),
            date(2023,8,15),
            date(2023,9,7),
            date(2023,9,18), # DayForMe
            date(2023,9,19),
            date(2023,10,2),
            date(2023,10,23),
            date(2023,11,1),
            date(2023,11,13),
            date(2023,12,25),
            date(2023,12,26),
            date(2023,12,27), #shutdown
            date(2023,12,28), #shutdown
            date(2023,12,29), #shutdown
            date(2024,1,1),
            date(2024,1,2) # DayForMe
        ]
        self.holidays['Canada'] = [
            date(2023,1,2), # New Years Day
            date(2023,1,3), # DayForMe
            date(2023,2,20), # DayForMe
            date(2023,2,23), # Family Day
            date(2023,4,7), # Good Friday
            date(2023,5,22), # Victoria Day
            date(2023,6,23), # St Jean Baptiste Day
            date(2023,6,30), # Canada Day
            date(2023,8,7), # Civic Holiday
            date(2023,9,4), # Labour Day
            date(2023,9,18), # DayForMe
            date(2023,9,29), # National Day Truth
            date(2023,10,9), # Thankgsiving Day
            date(2023,11,10), # Rememberance Day
            date(2023,12,23), # Christmas Eve
            date(2023,12,25), # Christmas Day
            date(2023,12,26), # Boxing Day
            date(2023,12,27), # Shutdown
            date(2023,12,28), # Shutdown
            date(2023,12,29), # Shutdown
            date(2024,1,1)
        ]
        self.holidays["Bulgaria"] = [# 2 days in Q1
            # TODO
            date(2023,10,16),
            date(2023,10,17) # Made up days
        ]
        self.holidays["Ukraine"] = [ # 1 day in Q1
            # TODO
            date(2023,10,16) # Made up days
        ]
        self.holidays["Poland"] = [ # 0 days in Q1
            # TODO
        ]
    # overriding abstract method
    def falls_on_holiday(self,some_date: date,location: str) -> bool:
        if location in self.holidays:
            if some_date in self.holidays[location]:
                print(f'Skipping {some_date}')
                return True;
        return False;

REMAINDER_OF_Q1 = ap.TimePeriod(
    name='q1_remaining',
    start_date=date.today(),
    end_date=date(2023,10,24)
)

Q2 = ap.TimePeriod(
    name='Q2',
    start_date=date(2023,10,25),
    end_date=date(2024,1,23)
)

holiday_schedule = HolidaySchedule()

features = ap.Features('features.yaml')
features.load_from_yaml_file()

teams = [
    ap.Team('GSD Team', 'gsd_team.yaml').load_from_yaml_file(),
    ap.Team('Skynet Team', 'skynet_team.yaml').load_from_yaml_file(),
]

for team in teams:
    ap.generate_capacity_sheet_for_team(team, REMAINDER_OF_Q1, holiday_schedule)
    ap.generate_capacity_sheet_for_team(team, Q2, holiday_schedule)

ap.generate_capacity_sheet_for_org("Whole Org", teams, REMAINDER_OF_Q1, holiday_schedule)
org_capacity_q2 = ap.generate_capacity_sheet_for_org("Whole Org", teams, Q2, holiday_schedule)    
df = org_capacity_q2.get_df()
x = df.loc[df['Front End'] == 'T']['Total'].sum()
print(f'Total (potential) Front End capacity {x}')
x = df.loc[df['Back End'] == 'T']['Total'].sum()
print(f'Total (potential) Back End capacity {x}')
x = df.loc[df['DevOps'] == 'T']['Total'].sum()
print(f'Total (potential) DevOps capacity {x}')

scheduler = ap.TeamScheduler(org_capacity_q2,features.get_epics())
schedule_results = scheduler.build_schedule()
for schedule_result in schedule_results:
    print(schedule_result)