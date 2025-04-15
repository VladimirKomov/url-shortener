import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ClickEventsModule } from './click-events/click-events.module';

@Module({
  imports: [ClickEventsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
