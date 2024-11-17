import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintTimelineComponent } from './sprint-timeline.component';

describe('SprintTimelineComponent', () => {
  let component: SprintTimelineComponent;
  let fixture: ComponentFixture<SprintTimelineComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintTimelineComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintTimelineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
