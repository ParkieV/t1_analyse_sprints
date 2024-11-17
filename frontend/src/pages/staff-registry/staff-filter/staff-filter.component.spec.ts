import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StaffFilterComponent } from './staff-filter.component';

describe('StaffFilterComponent', () => {
  let component: StaffFilterComponent;
  let fixture: ComponentFixture<StaffFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StaffFilterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StaffFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
