//
//  HUTRegExTool.swift
//  HUT
//
//  Created by Hut on 2021/10/18.
//  Copyright © 2021 HUT
//

import Foundation

struct ATRegExTool {
    
    enum ATRegExCheckType {
        case username
        case password
        case phonenumber
        case email
        case ipv4
        case ipv6
        
        var rexString: String {
            var regExStr = ""
            switch self {
            case .username:
                regExStr = ""
            case .password:
                regExStr = "^.*(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[~@#_^*%/.+:;=$&!])[0-9A-Za-z~@#_^*%/.+:;=$&!]{8,}$"
            case .phonenumber:
                regExStr = "^.*(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[~@#_^*%/.+:;=$&!])[0-9A-Za-z~@#_^*%/.+:;=$&!]{8,}$"
            case .email:
                regExStr = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
            case .ipv4:
                regExStr = "^((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)(\\.(?!$)|$)){4}$"
            case .ipv6:
                /// include 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
                regExStr = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
            }
            return regExStr
        }
    }

    func checkIsValid(checkType: ATRegExCheckType, targetString: String) -> Bool {
        let rexgexExpression = checkType.rexString
        let predicate = NSPredicate(format: "SELF MATCHES %@", rexgexExpression)
        if !predicate.evaluate(with: targetString) {
            return false
        } else {
            return true
        }
    }
}
