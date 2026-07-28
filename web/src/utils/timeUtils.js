const now = new Date();
const ACCUMULATION_HOUR = 12;

const formatHour = (date, withZulu = false) => {
  const hour = date.getHours();
  return hour;
};

export function getLatestTimeDate() {
  // Round down to the nearest hour
  now.setMinutes(0);
  now.setSeconds(0);
  now.setMilliseconds(0);

  // Format the date using Intl.DateTimeFormat
  const formatter = new Intl.DateTimeFormat("en-US", {
    month: "long",   
    day: "numeric",  
    year: "numeric",    
    //hour: "numeric", 
    //minute: "2-digit", 
    //hour12: true
  });

  return formatter.format(now).replace(",", "");
}

export function formatSensingTime() {
  const sensingTime = ACCUMULATION_HOUR;
  const sensingTimeR = ACCUMULATION_HOUR - 12;

  if (sensingTime < 12) {
    return `${sensingTime} AM`;
  }
  else {
    return `${sensingTimeR} PM`;
  }
}

export function formatSensingTimeECMWF() {
  const sensingTime = ACCUMULATION_HOUR - 4; // Shifted by 4 hours to accommodate earthkit-data requirements
  const sensingTimeR = ACCUMULATION_HOUR - 12;

  if (sensingTime < 12) {
    return `${sensingTime} AM`;
  }
  else {
    return `${sensingTimeR} PM`;
  }
}