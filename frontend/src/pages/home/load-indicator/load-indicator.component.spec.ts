import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadIndicatorComponent } from './load-indicator.component';

describe('LoadIndicatorComponent', () => {
  let component: LoadIndicatorComponent;
  let fixture: ComponentFixture<LoadIndicatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoadIndicatorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoadIndicatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
