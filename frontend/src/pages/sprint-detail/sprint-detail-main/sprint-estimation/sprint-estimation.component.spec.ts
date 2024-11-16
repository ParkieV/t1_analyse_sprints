import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintEstimationComponent } from './sprint-estimation.component';

describe('SprintEstimationComponent', () => {
  let component: SprintEstimationComponent;
  let fixture: ComponentFixture<SprintEstimationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintEstimationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintEstimationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
