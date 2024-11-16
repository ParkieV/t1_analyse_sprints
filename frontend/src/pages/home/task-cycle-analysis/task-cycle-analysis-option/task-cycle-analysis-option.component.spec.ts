import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskCycleAnalysisOptionComponent } from './task-cycle-analysis-option.component';

describe('TaskCycleAnalysisOptionComponent', () => {
  let component: TaskCycleAnalysisOptionComponent;
  let fixture: ComponentFixture<TaskCycleAnalysisOptionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskCycleAnalysisOptionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskCycleAnalysisOptionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
