import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintDetailMainComponent } from './sprint-detail-main.component';

describe('SprintDetailMainComponent', () => {
  let component: SprintDetailMainComponent;
  let fixture: ComponentFixture<SprintDetailMainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintDetailMainComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintDetailMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
