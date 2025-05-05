import {ConfigService} from '@nestjs/config';
import {createLogger} from "./utils/logger.util";

const logger = createLogger('MongoOptions')

export const getMongoUri = (configService: ConfigService): string => {
    const mongoUri = configService.get('MONGO_URL');

    if (!mongoUri) {
        logger.error('MONGO_URL is not defined');
        throw new Error('MONGO_URL is not defined');
    }

    return mongoUri;
}