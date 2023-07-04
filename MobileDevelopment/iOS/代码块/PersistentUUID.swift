//
//  PersistentUUID.swift
//  ShinePhone
//
//  Created by Hut on 2021/3/27.
//  Copyright © 2021 Growatt New Energy Technology CO.,LTD. All rights reserved.
//

import Foundation
import Security

/// 将app第一次运行生成的UUID存储于key chain, 作为设备的UUID
/// Base on https://github.com/objcio/keychain-item
final public class PersistentUUID {
    public static let `default` = PersistentUUID()

    public enum SWKeychainError: Error {
        case keychainError(status: OSStatus)
    }
    
    private let name: String;
    
    public init(name: String = "iWatchDevicePersistentIdentifier") {
        self.name = name
    }
    
    public func initialize() throws {
        if try get() == nil {
            try add(name: self.name, value: generateIdentifier())
        }
    }
    
    public func reset() throws {
        try set(identifier: generateIdentifier())
    }
    
    public func delete() throws {
        let item: [String:AnyObject] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: name as AnyObject
        ]
        
        let status = SecItemDelete(item as CFDictionary)
        if status != noErr && status != errSecItemNotFound {
            throw SWKeychainError.keychainError(status: status)
        }
    }
    
    public func get() throws -> String? {
        let query: [String:AnyObject] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: name as AnyObject,
            kSecMatchLimit as String: kSecMatchLimitOne,
            kSecReturnData as String: true as AnyObject
        ]
        
        var result: AnyObject? = nil
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        if status == errSecItemNotFound {
            return nil
        }
        
        if status != noErr {
            throw SWKeychainError.keychainError(status: status)
        }
        
        guard let data = result as? Data, let identifier = String(data: data, encoding: .utf8) else {
            return nil
        }
        
        return identifier
    }
    
    private func add(name: String, value: String) throws {
        let attributes: [String:AnyObject] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: name as AnyObject,
            kSecValueData as String: value.data(using: .utf8)! as AnyObject,
        ]
        
        let status = SecItemAdd(attributes as CFDictionary, nil)
        if status != noErr {
            throw SWKeychainError.keychainError(status: status)
        }
    }
    
    private func update(name: String, value: String) throws {
        let query: [String:AnyObject] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: name as AnyObject
        ]
        
        let attributes: [String:AnyObject] = [
            kSecValueData as String: value.data(using: .utf8)! as AnyObject,
        ]
        
        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)
        if status != noErr {
            throw SWKeychainError.keychainError(status: status)
        }
    }
    
    private func set(identifier: String) throws {
        if try get() == nil {
            try add(name: self.name, value: identifier)
        } else {
            try update(name: self.name, value: identifier)
        }
    }
    
    private func generateIdentifier() -> String {
        return UUID().uuidString
    }
}
