import {Module} from '@nestjs/common';
import {ClickEventsModule} from './click-events/click-events.module';
import {RabbitMQConfigModule} from "./rabbitmq.module";
import {ConfigModule} from "@nestjs/config";

@Module({
    imports: [
        // load config from .env
        ConfigModule.forRoot({ isGlobal: true }),
        ClickEventsModule,
        RabbitMQConfigModule
    ],

})
export class AppModule {
}
