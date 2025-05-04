import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import {getRmqOptions} from "./rabbitmq.options";
import {ConfigService} from "@nestjs/config";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  //get config
  const config = app.get(ConfigService);
  // Rabbit connection
  app.connectMicroservice(getRmqOptions(config))
  // Start microservice
  await app.startAllMicroservices()

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
