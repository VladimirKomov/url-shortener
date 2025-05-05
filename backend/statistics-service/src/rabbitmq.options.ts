import { RmqOptions, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';
import {createLogger} from "./utils/logger.util";

const logger = createLogger('RabbitOptions');

export const getRmqOptions = (configService: ConfigService): RmqOptions => {
    const user = configService.get('RABBITMQ_DEFAULT_USER');
    const pass = configService.get('RABBITMQ_DEFAULT_PASS');
    const host = configService.get('RABBITMQ_HOST');
    const port = configService.get('RABBITMQ_PORT');
    const vhost = configService.get('RABBITMQ_VHOST');
    const queue = configService.get('RABBITMQ_QUEUE_CLICK_EVENTS');

    if (!user || !pass || !host || !port || !vhost || !queue) {
        logger.error('Missing RabbitMQ config in .env');
        throw new Error('RabbitMQ connection config is incomplete');
    }

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
