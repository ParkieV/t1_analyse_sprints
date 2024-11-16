import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskCycleAnalysisChartComponent } from './task-cycle-analysis-chart.component';

describe('TaskCycleAnalysisChartComponent', () => {
  let component: TaskCycleAnalysisChartComponent;
  let fixture: ComponentFixture<TaskCycleAnalysisChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskCycleAnalysisChartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskCycleAnalysisChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
