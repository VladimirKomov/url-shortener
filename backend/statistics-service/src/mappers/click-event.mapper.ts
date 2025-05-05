import {ClickEvent, RawClickEvent} from "../events/click-event.dto";

export const mapRawClickEvent = (rawClickEvent: RawClickEvent): ClickEvent => (
    {
        ...rawClickEvent,
        timestamp: new Date(rawClickEvent.timestamp)
    }
)
