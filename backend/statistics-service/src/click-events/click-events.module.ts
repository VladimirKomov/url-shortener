import { Module } from '@nestjs/common';
import { ClickEventsService } from './click-events.service';
import { ClickEventsController } from './click-events.controller';

@Module({
  providers: [ClickEventsService],
  controllers: [ClickEventsController]
})
export class ClickEventsModule {}
