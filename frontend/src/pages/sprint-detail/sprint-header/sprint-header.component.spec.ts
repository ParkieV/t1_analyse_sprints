import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SprintHeaderComponent } from './sprint-header.component';

describe('SprintHeaderComponent', () => {
  let component: SprintHeaderComponent;
  let fixture: ComponentFixture<SprintHeaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SprintHeaderComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SprintHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
