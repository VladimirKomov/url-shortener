import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import {UrlClickConsumer} from "./url-click.consumer";

@Module({
  imports: [
      ConfigModule.forRoot({
        isGlobal: true,
      }),
  ],
  controllers: [
      UrlClickConsumer,
      AppController
  ],
  providers: [AppService],
})
export class AppModule {}
