import { RmqOptions, Transport } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';
import * as amqp from 'amqplib';

export function getRabbitConfig(config: ConfigService) {
    const user = config.get<string>('RABBITMQ_DEFAULT_USER');
    const pass = config.get<string>('RABBITMQ_DEFAULT_PASS');
    const host = config.get<string>('RABBITMQ_HOST');
    const port = config.get<string>('RABBITMQ_PORT');
    const vhost = config.get<string>('RABBITMQ_VHOST');
    const queue = config.get<string>('RABBITMQ_QUEUE_CLICK_EVENTS');
    const exchange = config.get<string>('RABBITMQ_EXCHANGE_CLICKS');
    const routingKey = config.get<string>('RABBITMQ_ROUTING_KEY_CLICKS');

    if (!user || !pass || !host || !port || !vhost || !queue || !exchange || !routingKey) {
        throw new Error('Missing RabbitMQ config in .env');
    }

    const uri = `amqp://${user}:${pass}@${host}:${port}/${encodeURIComponent(vhost)}`;

    return { uri, queue, exchange, routingKey };
}

export async function bindQueueToExchange(config: ConfigService) {
    const { uri, exchange, queue, routingKey } = getRabbitConfig(config);

    const connection = await amqp.connect(uri);
    const channel = await connection.createChannel();

    await channel.assertExchange(exchange, 'topic', { durable: true });
    await channel.assertQueue(queue, { durable: true });
    await channel.bindQueue(queue, exchange, routingKey);

    console.log(`Bound queue "${queue}" to exchange "${exchange}"`);

    await channel.close();
    await connection.close();
}

export const getRmqOptions = (config: ConfigService): RmqOptions => {
    const { uri, queue } = getRabbitConfig(config);

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
