import { TestBed } from '@angular/core/testing';

import { SprintDetailService } from './sprint-detail.service';

describe('SprintDetailService', () => {
  let service: SprintDetailService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SprintDetailService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
