import { RmqOptions, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';

export const getRmqOptions = (configService: ConfigService): RmqOptions => {
    const user = configService.get('RABBITMQ_DEFAULT_USER');
    const pass = configService.get('RABBITMQ_DEFAULT_PASS');
    const host = configService.get('RABBITMQ_HOST');
    const port = configService.get('RABBITMQ_PORT');
    const vhost = configService.get('RABBITMQ_VHOST');
    const queue = configService.get('RABBITMQ_QUEUE_CLICK_EVENTS');

    const uri = `amqp://${user}:${pass}@${host}:${port}${vhost}`;

    return {
        transport: Transport.RMQ,
        options: {
            urls: [uri],
            queue,
            queueOptions: {
                durable: true,
            },
        },
    };
};
