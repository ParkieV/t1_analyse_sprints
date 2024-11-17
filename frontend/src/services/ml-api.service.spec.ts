import { TestBed } from '@angular/core/testing';

import { MlApiService } from './ml-api.service';

describe('MlApiService', () => {
  let service: MlApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MlApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
