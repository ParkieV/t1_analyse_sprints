import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintsFiltersComponent } from './sprints-filters.component';

describe('SprintsFiltersComponent', () => {
  let component: SprintsFiltersComponent;
  let fixture: ComponentFixture<SprintsFiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintsFiltersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintsFiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
