import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskStagesChartComponent } from './task-stages-chart.component';

describe('TaskStagesChartComponent', () => {
  let component: TaskStagesChartComponent;
  let fixture: ComponentFixture<TaskStagesChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskStagesChartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskStagesChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
