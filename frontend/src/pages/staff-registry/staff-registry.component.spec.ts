import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StaffRegistryComponent } from './staff-registry.component';

describe('StaffRegistryComponent', () => {
  let component: StaffRegistryComponent;
  let fixture: ComponentFixture<StaffRegistryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StaffRegistryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StaffRegistryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
