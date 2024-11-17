import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintKanbanComponent } from './sprint-kanban.component';

describe('SprintKanbanComponent', () => {
  let component: SprintKanbanComponent;
  let fixture: ComponentFixture<SprintKanbanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintKanbanComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintKanbanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
