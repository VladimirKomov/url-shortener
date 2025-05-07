import {ConfigService} from '@nestjs/config';
import {createLogger} from "./utils/logger.util";

const logger = createLogger('MongoOptions')

export const getMongoUri = (config: ConfigService): string => {
    const user = config.get<string>('MONGO_USER');
    const pass = config.get<string>('MONGO_PASS');
    const host = config.get<string>('MONGO_HOST');
    const port = config.get<string>('MONGO_PORT');
    const dbName = config.get<string>('MONGO_DB_NAME');
    const options = config.get<string>('MONGO_OPTIONS');

    if (!user || !pass || !host || !port || !dbName) {
        logger.error('MONGO_URL is not defined');
        throw new Error('Incomplete MongoDB config');
    }

    let uri = `mongodb://${user}:${pass}@${host}:${port}/${dbName}`;
    if (options) {
        uri += `?${options}`;
    }

    return uri;
};