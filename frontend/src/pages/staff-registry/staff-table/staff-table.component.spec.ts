import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StaffTableComponent } from './staff-table.component';

describe('StaffTableComponent', () => {
  let component: StaffTableComponent;
  let fixture: ComponentFixture<StaffTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StaffTableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StaffTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
