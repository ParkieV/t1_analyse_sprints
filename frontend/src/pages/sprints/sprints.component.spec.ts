import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintsComponent } from './sprints.component';

describe('SprintsComponent', () => {
  let component: SprintsComponent;
  let fixture: ComponentFixture<SprintsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
