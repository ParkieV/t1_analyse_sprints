import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintDetailTasksComponent } from './sprint-detail-tasks.component';

describe('SprintDetailTasksComponent', () => {
  let component: SprintDetailTasksComponent;
  let fixture: ComponentFixture<SprintDetailTasksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintDetailTasksComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintDetailTasksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
