import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskCycleAnalysisComponent } from './task-cycle-analysis.component';

describe('TaskCycleAnalysisComponent', () => {
  let component: TaskCycleAnalysisComponent;
  let fixture: ComponentFixture<TaskCycleAnalysisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskCycleAnalysisComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskCycleAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
