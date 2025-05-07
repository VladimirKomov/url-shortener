import {ClickEventDto, ClickEventResponseDto, RawClickEventDto} from "../dto/click-event.dto";

export const mapRawClickEvent = (rawClickEvent: RawClickEventDto): ClickEventDto => {
    return {
        shortCode: rawClickEvent.short_code,
        ipAddress: rawClickEvent.ip_address,
        userAgent: rawClickEvent.user_agent,
        referer: rawClickEvent.referer,
        timestamp: new Date(rawClickEvent.timestamp)
    }
};

export const mapClickEventToResponse = (doc: any): ClickEventResponseDto => {
    return {
        shortCode: doc.shortCode,
        ipAddress: doc.ipAddress,
        userAgent: doc.userAgent,
        referer: doc.referer,
        timestamp: doc.timestamp ? doc.timestamp.toISOString() : null,
    }
}

