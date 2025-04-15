import { Test, TestingModule } from '@nestjs/testing';
import { ClickEventsService } from './click-events.service';

describe('ClickEventsService', () => {
  let service: ClickEventsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ClickEventsService],
    }).compile();

    service = module.get<ClickEventsService>(ClickEventsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
