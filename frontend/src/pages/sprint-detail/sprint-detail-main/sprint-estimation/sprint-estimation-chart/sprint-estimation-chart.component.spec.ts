import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintEstimationChartComponent } from './sprint-estimation-chart.component';

describe('SprintEstimationChartComponent', () => {
  let component: SprintEstimationChartComponent;
  let fixture: ComponentFixture<SprintEstimationChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintEstimationChartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintEstimationChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
