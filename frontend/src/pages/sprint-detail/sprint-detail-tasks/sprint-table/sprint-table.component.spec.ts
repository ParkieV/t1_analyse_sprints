import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintTableComponent } from './sprint-table.component';

describe('SprintTableComponent', () => {
  let component: SprintTableComponent;
  let fixture: ComponentFixture<SprintTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
