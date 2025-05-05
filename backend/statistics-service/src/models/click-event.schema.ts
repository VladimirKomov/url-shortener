import {Prop, Schema, SchemaFactory} from '@nestjs/mongoose';
import {Document} from "mongoose";


export type ClickEventDocument = ClickEventEntity & Document;

@Schema()
export class ClickEventEntity {
    @Prop({required: true})
    shortCode: string;
    @Prop({required: true})
    ipAddress: string;
    @Prop()
    userAgent?: string;
    @Prop()
    referer?: string;
    @Prop({required: true})
    timestamp: Date;

}

export const ClickEventSchema = SchemaFactory.createForClass(ClickEventEntity);