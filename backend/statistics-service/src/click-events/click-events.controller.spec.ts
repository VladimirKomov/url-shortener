import { Test, TestingModule } from '@nestjs/testing';
import { ClickEventsController } from './click-events.controller';

describe('ClickEventsController', () => {
  let controller: ClickEventsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ClickEventsController],
    }).compile();

    controller = module.get<ClickEventsController>(ClickEventsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
