import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadIndicatorScaleComponent } from './load-indicator-scale.component';

describe('LoadIndicatorScaleComponent', () => {
  let component: LoadIndicatorScaleComponent;
  let fixture: ComponentFixture<LoadIndicatorScaleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoadIndicatorScaleComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoadIndicatorScaleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
