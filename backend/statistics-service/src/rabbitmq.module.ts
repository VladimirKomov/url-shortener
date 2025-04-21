import { Module } from '@nestjs/common';
import { RabbitMQModule as RabbitMQCoreModule } from '@golevelup/nestjs-rabbitmq';
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
    imports: [
        RabbitMQCoreModule.forRootAsync({
            imports: [ConfigModule],
            useFactory: async (configService: ConfigService) => {
                const host = configService.get('RABBITMQ_HOST');
                const port = configService.get('RABBITMQ_PORT');
                const user = configService.get('RABBITMQ_DEFAULT_USER');
                const pass = configService.get('RABBITMQ_DEFAULT_PASS');
                const vhost = configService.get('RABBITMQ_VHOST');
                const queue = configService.get('RABBITMQ_QUEUE_CLICK_EVENTS');

                const uri = `amqp://${user}:${pass}@${host}:${port}${vhost}`;

                return {
                    uri,
                    queue,
                    queueOptions: {
                        durable: false,
                    },
                    exchanges: [
                        {
                            name: 'clicks_exchange',
                            type: 'topic',
                        },
                    ],
                };
            },
            inject: [ConfigService],
        }),
    ],
    exports: [RabbitMQCoreModule],
})
export class RabbitMQConfigModule {}
