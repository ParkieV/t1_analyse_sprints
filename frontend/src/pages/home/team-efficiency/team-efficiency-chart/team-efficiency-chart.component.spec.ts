import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeamEfficiencyChartComponent } from './team-efficiency-chart.component';

describe('TeamEfficiencyChartComponent', () => {
  let component: TeamEfficiencyChartComponent;
  let fixture: ComponentFixture<TeamEfficiencyChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeamEfficiencyChartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TeamEfficiencyChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
